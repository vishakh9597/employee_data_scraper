## Features
- Fetches employee data from an external API
- Validates required fields in the API response
- Normalizes employee data based on business rules
- Handles invalid phone numbers
- Generates a cleaned CSV output file
- Includes basic unit tests using unittest and mocking

## Business Rules Implemented
- **Full Name** is created by combining first name and last name
- **Designation** is derived from years of experience:
  - Less than 3 years → System Engineer
  - 3 to 5 years → Data Engineer
  - 6 to 10 years → Senior Data Engineer
  - More than 10 years → Lead
- Phone numbers containing `x` are marked as `Invalid Number`
- Hire date column is included and kept empty if not provided by the API
