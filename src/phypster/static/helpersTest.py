from src import app, db, logger


def clearTables():
    with app.app_context():
        try:
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
        except Exception as e:
            logger.error("clearTables: error = {0}".format(e))
