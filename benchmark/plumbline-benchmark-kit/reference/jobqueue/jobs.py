"""Small persistent job lifecycle; one connection per Store instance."""
import sqlite3

class StateError(ValueError):
    """The requested transition is not valid."""

class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path, timeout=5)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY, state TEXT NOT NULL, attempt INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS attempts (
                job_id TEXT NOT NULL, number INTEGER NOT NULL, state TEXT NOT NULL,
                PRIMARY KEY(job_id, number));
        """)
        self.db.execute("""CREATE TABLE IF NOT EXISTS retry_keys (
            job_id TEXT NOT NULL, request_id TEXT NOT NULL,
            PRIMARY KEY(job_id, request_id))""")
        self.db.commit()

    def close(self):
        self.db.close()

    def submit(self, job_id):
        with self.db:
            self.db.execute("INSERT INTO jobs VALUES (?, 'queued', 1)", (job_id,))
            self.db.execute("INSERT INTO attempts VALUES (?, 1, 'queued')", (job_id,))
        return self.get(job_id)

    def get(self, job_id):
        row = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        return dict(row)

    def history(self, job_id):
        self.get(job_id)
        return [dict(row) for row in self.db.execute(
            "SELECT number, state FROM attempts WHERE job_id=? ORDER BY number", (job_id,))]

    def _transition(self, job_id, expected, target):
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            job = self.get(job_id)
            if job['state'] not in expected:
                raise StateError(job['state'])
            self.db.execute("UPDATE jobs SET state=? WHERE id=?", (target, job_id))
            self.db.execute("UPDATE attempts SET state=? WHERE job_id=? AND number=?",
                            (target, job_id, job['attempt']))
        return self.get(job_id)

    def start(self, job_id):
        return self._transition(job_id, {'queued'}, 'running')

    def complete(self, job_id):
        return self._transition(job_id, {'running'}, 'complete')

    def fail(self, job_id):
        return self._transition(job_id, {'running'}, 'failed')

    def cancel(self, job_id):
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            job = self.get(job_id)
            if job['state'] in {'cancelling', 'cancelled'}:
                return job
            targets = {'queued': 'cancelled', 'running': 'cancelling'}
            if job['state'] not in targets:
                raise StateError(job['state'])
            state = targets[job['state']]
            self.db.execute("UPDATE jobs SET state=? WHERE id=?", (state, job_id))
            self.db.execute("UPDATE attempts SET state=? WHERE job_id=? AND number=?",
                            (state, job_id, job['attempt']))
            return self.get(job_id)

    def ack_cancel(self, job_id):
        return self._transition(job_id, {'cancelling', 'cancelled'}, 'cancelled')

    def retry(self, job_id, request_id):
        if not isinstance(request_id, str) or not request_id:
            raise ValueError('request_id must be a non-empty string')
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            job = self.get(job_id)
            if self.db.execute("SELECT 1 FROM retry_keys WHERE job_id=? AND request_id=?",
                               (job_id, request_id)).fetchone():
                return job
            if job['state'] != 'failed':
                raise StateError(job['state'])
            number = job['attempt'] + 1
            self.db.execute("INSERT INTO attempts VALUES (?, ?, 'queued')", (job_id, number))
            self.db.execute("UPDATE jobs SET state='queued', attempt=? WHERE id=?", (number, job_id))
            self.db.execute("INSERT INTO retry_keys VALUES (?, ?)", (job_id, request_id))
            return self.get(job_id)
