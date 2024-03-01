import axios from "axios";
import { useState } from "react";


export default function Hello() {
    const [message, setMessage] = useState('');

    const handleClick = async () => {
        try {
          const response = await axios.get('http://localhost:8000/api/get-message/');
          setMessage(response.data.message);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
    };


    return (
        <div>
        <button onClick={handleClick}>Get Message</button>
        {message && <p>{message}</p>} 
        </div>
    );

}