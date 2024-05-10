import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './appointments.css'; // Importe o arquivo CSS

const AppointmentsPage = ({ user }) => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/my_scheduler_api/clients/${user}/appointments/`);
        setAppointments(response.data.appointments);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      }
    };
    fetchAppointments();
  }, [user]);

  return (

    <div className="appointments-container">
      <h2 className="appointments-title">Appointments</h2>
      <h3 className="appointments-subtitle">Appointments made by you:</h3>
      <ul className="appointments-list">
        {appointments && appointments.map((appointment) => (
          <li key={appointment.id} className="appointments-item">
            <span className="appointments-text">Employee: {appointment.employee}</span>
            <span className="appointments-text">Service: {appointment.service}</span>
            <span className="appointments-text">Date: {appointment.date}</span>
            <span className="appointments-text">Time: {appointment.time}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AppointmentsPage;
