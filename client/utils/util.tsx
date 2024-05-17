import { NextRouter } from "next/router";
import { useEffect, useState } from "react";

export function useAuth() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [username, setUsername] = useState("");

    const updateAuthStatus = () => {
        const token = localStorage.getItem('authToken');
        const user = localStorage.getItem('username');
        if (token && user) {
            setIsLoggedIn(true);
            setUsername(user);
        } else {
            setIsLoggedIn(false);
            setUsername("");
        }
    };

    useEffect(() => {
        updateAuthStatus();

        const handleStorageChange = () => {
            updateAuthStatus();
        };

        window.addEventListener('storage', handleStorageChange);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, []);

    return { isLoggedIn, username, updateAuthStatus };
}

export function logout(updateAuthStatus: () => void, router: NextRouter) {
    localStorage.removeItem('authToken');
    localStorage.removeItem('username');
    updateAuthStatus();
    router.push('/auth/login');
}