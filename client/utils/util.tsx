import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export function useAuth() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [username, setUsername] = useState("");

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        const user = localStorage.getItem('username');
        if (token && user) {
        setIsLoggedIn(true);
        setUsername(user);
        }
    }, []);

    return { isLoggedIn, username };
}

export function logout(router) {
    localStorage.removeItem('authToken');
    localStorage.removeItem('username');
    router.push('/auth/login');
}