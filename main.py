import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class PersonRecord(BaseModel):
    name: str
    role: str
    info: str

    @staticmethod
    def from_dict(data: dict):
        record = PersonRecord(**data)
        return record


class Problem(BaseModel):
    detail: str


class Database:
    def __init__(self):
        self._data: list = []

    def load_from_filename(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = PersonRecord.from_dict(record)
                self._data.append(obj)

    def delete(self, id_person: int):
        if 0 < id_person >= len(self._data):
            return
        self._data.pop(id_person)

    def add(self, person: PersonRecord):
        self._data.append(person)

    def get(self, id_person: int):
        if 0 < id_person >= len(self._data):
            return
        return self._data[id_person]

    def get_all(self) -> list[PersonRecord]:
        return self._data

    def update(self, id_person: int, person: PersonRecord):
        if 0 < id_person >= len(self._data):
            return
        self._data[id_person] = person

    def count(self) -> int:
        return len(self._data)


db = Database()
db.load_from_filename('names.json')

app = FastAPI(title="Herci API", version="0.1", docs_url="/docs")

app.is_shutdown = False


@app.get("/people", response_model=list[PersonRecord], description="Vrátí seznam herců")
async def get_person():
    return db.get_all()


@app.get("/people/{id_person}", response_model=PersonRecord)
async def get_person(id_person: int):
    return db.get(id_person)


@app.post("/people", response_model=PersonRecord, description="Přidáme herce do DB")
async def post_person(person: PersonRecord):
    db.add(person)
    return person


@app.delete("/people/{id_person}", description="Sprovodíme herce ze světa", responses={
    404: {'model': Problem}
})
async def delete_person(id_person: int):
    person = db.get(id_person)
    if person is None:
        raise HTTPException(404, "Herec neexistuje")
    db.delete(id_person)
    return {'status': 'smazano'}


@app.patch("/people/{id_person}", description="Aktualizujeme herce do DB", responses={
    404: {'model': Problem}
})
async def update_person(id_person: int, updated_person: PersonRecord):
    person = db.get(id_person)
    if person is None:
        raise HTTPException(404, "Herec neexistuje")
    db.update(id_person, updated_person)
    return {'old': person, 'new': updated_person}