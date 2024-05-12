import React, { useState, useEffect } from 'react';
import './appointments.css'; // Importe o arquivo CSS
import axios from 'axios';

const ServiceAppointments = ({ clientId, serviceId }) => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/my_scheduler_api/clients/${clientId}/services/${serviceId}/appointments/`);
        setAppointments(response.data);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      }
    };
    fetchAppointments();
  }, [clientId, serviceId]);

  return (
    <div className="appointments-container">
      <h2 className="appointments-title" >Marcações para o seu serviço</h2>
      <ul className="appointments-list">
        { appointments && appointments.map((appointment) => (
          <li key={appointment.id} className="appointments-item" >
           <li className="appointments-text"> Nome do Cliente: {appointment.client.name} </li>
           <li className="appointments-text"> Data: {appointment.time}</li>
           <li className="appointments-text">Hora: {appointment.date}</li> 
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ServiceAppointments;
