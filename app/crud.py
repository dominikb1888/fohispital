from sqlalchemy.orm import Session

from . import models, schemas


# TODO: Make independent from FHIR Resource Type

def get_resource(db: Session, res_id: int):
    return db.query(models.Resource).filter(models.Resource.id == res_id).first()


def get_resource_by_key(db: Session, key: str):
    return db.query(models.Resource).filter(models.Resource.key == key).first()


def get_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resource).offset(skip).limit(limit).all()

def create_resource(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(resource)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource
