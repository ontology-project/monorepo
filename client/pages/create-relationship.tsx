import React, { useState } from 'react';
import axios from 'axios';

interface CreateNodeWithRelationshipFormProps {}

interface ResponseData {
  name?: string;
  error?: string;
}

const CreateNodeWithRelationshipForm: React.FC<CreateNodeWithRelationshipFormProps> = () => {
  const [nodeName, setNodeName] = useState('');
  const [otherNodeId, setOtherNodeId] = useState('');
  const [relationshipType, setRelationshipType] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/api/create-relationship/', {
        name: nodeName,
        otherNodeId: otherNodeId,
        relationshipType: relationshipType
      });

      setMessage(`Node created with name: ${response.data.name}`);
      setNodeName('');
      setOtherNodeId('');
      setRelationshipType('');

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
      <div>
        <label htmlFor="nodeName">Node Name:</label>
        <input
          type="text"
          id="nodeNameInput"
          value={nodeName}
          onChange={(e) => setNodeName(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="otherNodeId">Other Node ID:</label>
        <input
          type="text"
          id="otherNodeIdInput"
          value={otherNodeId}
          onChange={(e) => setOtherNodeId(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="relationshipType">Relationship Type:</label>
        <input
          type="text"
          id="relationshipTypeInput"
          value={relationshipType}
          onChange={(e) => setRelationshipType(e.target.value)}
          required
        />
      </div>
      <button type="submit">Create Node with Relationship</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default CreateNodeWithRelationshipForm;
