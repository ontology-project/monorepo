// components/AuthCheck.tsx
import React from 'react';
import { useAuth } from '../utils/util';
import styles from '../styles/Home.module.css'

const AuthCheck: React.FC = ({ children }) => {
  const { isLoggedIn, username } = useAuth();

  if (!isLoggedIn) {
    return (
      <div className={styles.container}>
        <main className={styles.main}>
          <h1 className={styles.title}>
            Please <a href="/auth/login">login</a> to continue.
          </h1>
        </main>
      </div>
    );
  }

  return <>{children}</>;
};

export default AuthCheck;
