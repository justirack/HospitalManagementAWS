# HospitalManagementAWS

This project will re-create the project found in my HospitalManagement repository but in aws.<br>
See original project link <a href="https://github.com/justirack/HospitalManagement">here</a> <br>
The project will use APIGateway to create the endpoints where requests will be sent, and will be backed by lambda functions. Data will be stored in multiple dynamoDB tables, with one for each of patients, doctors and appointments respectively.

# Tentative Architecture
The following draw.io diagram contains the initial architecture diagram for patients and doctors. The diagram will be updated to include appointments once patients and doctors are complete.

![Alt](images/hospital_manager_diagram.svg)


# Endpoint Request Specifications
## user/add
The add user endpoint expects the following:
- First name
- Last name
- Date of birth (yyyy-mm-dd)
- Phone number (xxx)xxx-xxxx
- User type (patient or doctor)

Sample JSON:
```json
{
 "first_name": "Justin",
 "last_name": "Rackley",
 "date_of_birth": "2002-02-09",
 "phone_number": "(123)456-7890",
 "user_type": "patient"
}
```






## patient/add
The add patient endpoint expects the patients first name, last name and date of birth in <code>yyyy-mm-dd</code> format as the body of the request.<br>
See sample JSON below:
 
``` json
{
  "first_name":"Justin",
  "last_name":"Rackley",
  "date_of_birth":"2002-02-09"
}
```

## patient/get
The get patient endpoint expects the patients id ad a query parameter in the following format.<br>
```
{
  id="12345678-1234-1234-123456789012"
}
```

## patient/update
The update endpoint expects the patient id along with any combination of the patients first name, last name or date of birth in the <code>yyyy-mm-dd</code> format as the body of the request. Whatever data is passed will be updated and used as the new values in the database<br>
See sample JSON blobs below:

``` json
{
  "id":"1234",
  "first_name":"Justin"
}
```

``` json
{
  "id":"1234",
  "last_name":"Rackley",
  "date_of_birth":"2002-02-09"
}
```

``` json
{
  "id":"1234",
  "first_name":"Justin",
  "last_name":"Rackley",
  "date_of_birth":"2002-02-09"
}
```
