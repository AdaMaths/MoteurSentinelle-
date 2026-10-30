from services import firestore_storage


class FakeDocument:
    def __init__(self):
        self.get_timeout = None
        self.set_timeout = None

    def get(self, timeout=None):
        self.get_timeout = timeout
        return type("Snapshot", (), {"exists": False})()

    def set(self, data, timeout=None):
        self.set_timeout = timeout


class FakeCollection:
    def __init__(self):
        self.document_ref = FakeDocument()
        self.stream_timeout = None

    def document(self, document_id):
        return self.document_ref

    def stream(self, timeout=None):
        self.stream_timeout = timeout
        return []


class FakeFirestoreClient:
    def __init__(self):
        self.collections = {}

    def collection(self, name):
        self.collections[name] = FakeCollection()
        return self.collections[name]


def test_firestore_initialization_defers_network_calls(monkeypatch):
    database = FakeFirestoreClient()
    monkeypatch.setattr(firestore_storage.firebase_admin, "get_app", lambda: object())
    monkeypatch.setattr(
        firestore_storage.firestore, "client", lambda app: database
    )

    storage = firestore_storage.FirestoreStorage(project_id="test-project")

    motor_collection = database.collections["motors"]
    assert motor_collection.document_ref.get_timeout is None

    assert storage.list_motors() == []
    assert motor_collection.document_ref.get_timeout == (
        firestore_storage.FIRESTORE_REQUEST_TIMEOUT_SECONDS
    )
    assert motor_collection.document_ref.set_timeout == (
        firestore_storage.FIRESTORE_REQUEST_TIMEOUT_SECONDS
    )
    assert motor_collection.stream_timeout == (
        firestore_storage.FIRESTORE_REQUEST_TIMEOUT_SECONDS
    )
