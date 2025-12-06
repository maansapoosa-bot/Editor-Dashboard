# Edi_Stats - Wagtail CMS Dashboard

A beginner-friendly content management dashboard built with Wagtail, Django, and Chart.js. This project provides a visual overview of editorial performance, including post statistics, author activity, and publication trends.

## Features

- **Dashboard Overview**: Quick stats on live posts, draft posts, and the latest publication date.
- **Visual Analytics**:
  - **Posts by Author**: Doughnut chart showing content distribution among authors.
  - **Posts Over Time**: Line chart tracking publication frequency.
  - **Top Editors**: Bar chart highlighting the most active contributors.


## Tech Stack

- **Backend**: Python, Django, Wagtail CMS
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js

## Setup Instructions


2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Dashboard**:
   - Go to `http://127.0.0.1:8000/admin/` and log in.
   - Navigate to the "Dashboard" menu item to view the stats.

## Project Structure

- `home/`: Contains the main application logic, models, and templates.
  - `templates/home/stats_dashboard.html`: The main dashboard template.
  - `wagtail_hooks.py`: Registers the dashboard in the Wagtail admin menu.
  - `views.py`: Handles the logic for fetching and processing dashboard data.
- `cms_stats/`: Project configuration settings.

## License

This project is open-source and available for use and modification.
