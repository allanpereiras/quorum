# Questions

1. Discuss your strategy and decisions implementing the application. 
Please, consider time complexity, effort cost, technologies used and any other 
variable that you understand important on your development process.

This project focus on creating a user-friendly and modern application while 
prioritizing efficiency, effort, and maintainability. 

### Technology Stack:

- Backend: Django (Python web framework)
- Frontend: Bulma (CSS framework)
- Charts: Charts.css (CSS charting library)
- Containerization: Docker

I explicitly avoided using CDNs to include the CSS resources.  
While CDNs improve performance in some cases, they can introduce privacy 
concerns and potential security vulnerabilities. 
Including resources directly within the project maintains more control over 
their delivery and updates.

### Data Population:

#### Management Command
A reusable Python management command (load_samples.py) 
was created to populate the database with sample data.

#### Pandas Library 
Pandas was chosen for its efficiency in reading, manipulating, 
and loading large datasets from CSV files.

I encountered an inconsistency in the "Bills" CSV where a row had an unknown 
Legislator ID (sponsor_id). To avoid foreign key constraint issues, this ID 
was replaced with an existing valid one. 
A more robust solution in production would involve identifying and handling 
missing or inconsistent data more gracefully.

2. How would you change your solution to account for future columns that might 
be requested, such as “Bill Voted On Date” or“Co-Sponsors”?

### Scalability for Future Changes would involve:

- Database Schema updates: New data columns would require creating database 
migrations using Django's migration framework.
- Data Population: Depending on the data source, various methods can be employed:
Management Commands: Existing or new management commands can be used to 
populate the database with the new data.
Fixtures: Fixtures can be created to represent the new data structure.
- Updating Views and Templates: Views responsible for retrieving data 
(e.g., BillsView.get_bills_data, BillsView.get_legislators_data) might need 
adjustments to handle the new data structure.
HTML templates displaying charts and tables would require updates to reflect 
the new data columns.


3. How would you change your solution if instead of receiving CSVs of data, 
you were given a list of legislators or bills that you should generate a CSV for?

That would require to code a new feature for exporting data which would be
probably based on the python built-in csv library or other option such as 
the Pandas library.


4. How long did you spend working on the assignment?

Around 8 hours were spent over two days (April 23rd and 24th, 2024).
Most of the time was dedicated to refining the UI and experimenting with Bulma
and the Charts.css CSS Framework.