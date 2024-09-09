Ghost Name Picker
==========================

Layout
------

 * `app.yaml` - Configure App Engine to serve the Ghost Name Picker.
 * `main.py` - The default Python entry-point for Ghost Name Picker on App Engine.
 * `modules.py` Helper functions to immitate DB behaviour.
 * `requirements.txt` - Third-party libaries that will be installed automatically when Ghost Name Picker is deployed.
 * `settings.py` - Custom settings for Flask.


Local development
----------
    for OAuth to work, both
    GOOGLE_CLIENT_ID and
    GOOGLE_CLIENT_SECRET
    need to be set in app.yaml


    setup a local venv

    source .venv/Scripts/activate
    pip install -r requirements.txt
    python main.py

    The development server then should start running on http://127.0.0.1:5000




Deployment
----------

    gcloud app deploy --project [PROJECT_ID] app.yaml
