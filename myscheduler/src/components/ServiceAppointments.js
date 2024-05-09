import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ServiceAppointments from './ServiceAppointments';

const AppointmentPage = ({ clientId }) => {
  const [services, setServices] = useState([]);
  const [selectedServiceId, setSelectedServiceId] = useState(null);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await axios.get(`/api/clients/${clientId}/services/`);
        setServices(response.data);
      } catch (error) {
        console.error('Failed to fetch services:', error);
      }
    };
    fetchServices();
  }, [clientId]);

  return (
    <div>
      <h2>Appointments</h2>
      <h3>Services</h3>
      <ul>
        {services.map((service) => (
          <li key={service.id}>
            <button onClick={() => setSelectedServiceId(service.id)}>{service.name}</button>
          </li>
        ))}
      </ul>
      {selectedServiceId && (
        <ServiceAppointments clientId={clientId} serviceId={selectedServiceId} />
      )}
    </div>
  );
};

export default AppointmentPage;
