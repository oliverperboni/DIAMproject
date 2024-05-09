import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AppointmentsPage = ({ user }) => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/clients/${user}/appointments/`);
        setAppointments(response.data.appointments);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      }
    };
    fetchAppointments();
  }, [user]);

  return (
    <div>
      <h2>Appointments</h2>
      <h3>Appointments made by you:</h3>
      <ul>
        {appointments.map((appointment) => (
          <li key={appointment.id}>
            Employee: {appointment.employee}<br />
            Service: {appointment.service}<br />
            Date: {appointment.date}<br />
            Time: {appointment.time}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AppointmentsPage;
