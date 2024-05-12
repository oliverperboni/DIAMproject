import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './appointments.css'; // Importe o arquivo CSS
import ServiceAppointments from './ServiceAppointments';

const AppointmentsPage = ({ user }) => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/my_scheduler_api/clients/${user}/appointments/`);
        setAppointments(response.data);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      }
    };
    fetchAppointments();
  }, [user]);

  const deleteAppointment = async (appointmentId) => {
    try {
      await axios.post(`http://127.0.0.1:8000/my_scheduler_api/appointment/${appointmentId}/delete/`);
      setAppointments(appointments.filter(appointment => appointment.id !== appointmentId));
      console.log('Appointment deleted successfully');
    } catch (error) {
      console.error('Failed to delete appointment:', error);
    }
  };

  return (
    <div className="appointments-container">
      <h2 className="appointments-title">Marcações</h2>
      <h3 className="appointments-subtitle">Marcações feitas por você:</h3>
      <ul className="appointments-list">
        {appointments && appointments.map((appointment) => (
          <li key={appointment.id} className="appointments-item">
            <li className="appointments-text">Empresa: {appointment.service.name}</li> 
            <li className="appointments-text">Data : {appointment.date}</li>
            <li className="appointments-text">Hora : {appointment.time}</li>
            <button onClick={() => deleteAppointment(appointment.id)}>Excluir</button>
          </li>
        ))}
      </ul>
      <ServiceAppointments clientId={user} serviceId={user} />
    </div>
  );
};

export default AppointmentsPage;
