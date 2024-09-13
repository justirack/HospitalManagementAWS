import React, {useState} from 'react';

async function createUser(payload) {
    const url = "https://dvhzr0xw4j.execute-api.us-west-2.amazonaws.com/user/v1/user/add"

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response)
        .then(data => {
            console.log(data.status)
        })
        .catch(error => {
            console.error(error);
            alert('Failed to retrieve data. Please try again later.');
        });
}

export default function CreateUserForm() {
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();
    const [dateOfBirth, setDateOfBirth] = useState();
    const [phoneNumber, setPhoneNumber] = useState();
    const [userType, setUserType] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        await createUser({
            "first_name": firstName,
            "last_name": lastName,
            "date_of_birth": dateOfBirth,
            "phone_number": phoneNumber,
            "user_type": userType
        });
    }

    return(
        <div className="create-user-wrapper">
            <h1>Please enter user information.</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    <p>First Name</p>
                    <input type="text" required onChange={e => setFirstName(e.target.value)}/>
                </label>
                <label>
                    <p>Last Name</p>
                    <input type="text" required onChange={e => setLastName(e.target.value)}/>
                </label>
                <label>
                    <p>Date of Birth</p>
                    <input type="date" required onChange={e => setDateOfBirth(e.target.value)}/>
                </label>
                <label>
                    <p>Phone Number</p>
                    <input type="tel" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" placeholder="111-111-1111" required onChange={e => setPhoneNumber(e.target.value)}/>
                </label>
                <label>
                    <p>User Type</p>
                    {/* TODO */}
                    {/* Remove the hard coded values for patient and doctor below */}
                    <input type="radio" name="user_type" required onChange={e => setUserType('patient')}/>
                    <label className="user-type-label">Patient</label>
                    <input type="radio" name="user_type" required onChange={e => setUserType('doctor')}/>
                    <label className="user-type-label">Doctor</label>
                </label>
                <div>
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    )
}

