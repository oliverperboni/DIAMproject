import React, { useState } from 'react';
import Login from './components/Login';
import AppointmentsPage from './components/AppointmentsPage';

const App = () => {
  const [user, setUser] = useState(null);

  const handleLogin = (user) => {
    setUser(user);
  };

  return (
    <div>
      {user ? (
        <AppointmentsPage user={user} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;
