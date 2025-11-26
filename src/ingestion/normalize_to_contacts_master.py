from api.database import SessionLocal
from api.models import MasterData, ContactsMaster


BATCH_SIZE = 5000


def map_row(row: dict, source_file: str):
    nd = row or {}
    rd = row or {}

    person_name = nd.get("person_name") or nd.get("full_name")
    first_name = (
        nd.get("person_first_name_unanalyzed")
        or nd.get("first_name")
    )
    last_name = (
        nd.get("person_last_name_unanalyzed")
        or nd.get("last_name")
    )

    email = nd.get("person_email") or nd.get("email")
    phone = nd.get("person_phone") or nd.get("phone")

    city = nd.get("person_city") or nd.get("city")
    state = nd.get("person_state") or nd.get("state")
    country = nd.get("person_country") or nd.get("country")

    company = nd.get("company_name") or nd.get("company")
    job_title = nd.get("job_title") or nd.get("person_title")
    domain = nd.get("company_domain") or nd.get("domain")
    industry = nd.get("industry")

    seniority_level = nd.get("seniority") or nd.get("seniority_level")
    experience_years = nd.get("experience_years")

    linkedin_url = (
        nd.get("person_linkedin_url")
        or nd.get("linkedin_url")
    )
    facebook_url = nd.get("facebook_url")
    twitter_url = nd.get("twitter_url")

    source_row_id = nd.get("_id") or nd.get("id")

    return ContactsMaster(
        source_file=source_file,
        source_row_id=source_row_id,
        person_name=person_name,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        city=city,
        state=state,
        country=country,
        company=company,
        job_title=job_title,
        domain=domain,
        industry=industry,
        seniority_level=seniority_level,
        experience_years=experience_years,
        linkedin_url=linkedin_url,
        facebook_url=facebook_url,
        twitter_url=twitter_url,
        raw_data=rd,
        normalized_data=nd,
    )


def run_migration():
    db = SessionLocal()
    try:
        last_id = 0
        while True:
            rows = (
                db.query(MasterData)
                .filter(MasterData.id > last_id)
                .order_by(MasterData.id)
                .limit(BATCH_SIZE)
                .all()
            )

            if not rows:
                break

            objs = []
            for r in rows:
                obj = map_row(r.normalized_data, r.source_file)
                objs.append(obj)

            db.bulk_save_objects(objs)
            db.commit()

            last_id = rows[-1].id
            print(f"Migrated up to master_data.id = {last_id}")

        print("✅ Finished migrating to contacts_master")

    finally:
        db.close()


if __name__ == "__main__":
    run_migration()
