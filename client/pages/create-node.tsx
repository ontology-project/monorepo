import React, { useState } from 'react';
import axios from 'axios';

interface CreateNodeFormProps {}

interface ResponseData {
  name?: string;
  error?: string;
}

const CreateNodeForm: React.FC<CreateNodeFormProps> = () => {
  const [nodeName, setNodeName] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/api/create-node/', {
        name: nodeName
      });

      setMessage(`Node created with name: ${response.data.name}`);
      setNodeName('');

    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setMessage(`Error: ${error.response.data.error}`);
      } else {
        console.error('Unexpected error:', error);
        setMessage('An unexpected error occurred.');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter node name"
        value={nodeName}
        onChange={(e) => setNodeName(e.target.value)}
      />
      <button type="submit">Create Node</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default CreateNodeForm;
