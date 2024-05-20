import { NextRouter } from "next/router";
import { useEffect, useRef, useState } from "react";
import { imageApiPost } from "./api";

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

export const useFileUpload = () => {
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [uploadResponse, setUploadResponse] = useState<any>(null);
    const [isUploaded, setIsUploaded] = useState(false);
    const inputFileRef = useRef<HTMLInputElement>(null);
  
    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const files = event.target.files;
      if (files) {
        setFile(files[0]);
        setIsUploaded(false);
      }
    };
  
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      if (file) {
        setLoading(true);
        try {
          const response = await imageApiPost('api/import-excel', file);
          setUploadResponse(response);
          setMessage('Upload success!');
          setIsUploaded(true);
        } catch (error: any) {
          setMessage(error.message);
        } finally {
          setFile(null);
          setLoading(false);
          if (inputFileRef.current) {
            inputFileRef.current.value = '';
          }
        }
      }
    };
  
    return {
      file,
      message,
      loading,
      uploadResponse,
      isUploaded,
      inputFileRef,
      handleFileChange,
      handleSubmit,
      setUploadResponse,
    };
  };