def register_routes(api, app):
    from app.person import register_routes as attach_person_routes

    # Add routes
    attach_person_routes(api, app)
