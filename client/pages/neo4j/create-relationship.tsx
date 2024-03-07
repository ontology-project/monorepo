import React, { useState } from 'react';
import { Box, Heading, FormControl, FormLabel, Input, Button, Select } from '@chakra-ui/react';
import { apiPost } from '../../utils/api';
import { NODE_TYPES, RELATIONSHIPS } from '../../utils/constants';

interface CreateNodeWithRelationshipFormProps {}



const CreateNodeWithRelationshipForm: React.FC<CreateNodeWithRelationshipFormProps> = () => {
  const [name, setName] = useState('');
  const [nodeType, setNodeType] = useState('');
  const [otherName, setOtherName] = useState('');
  const [otherType, setOtherType] = useState('');
  const [relationshipType, setRelationshipType] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await apiPost('api/create-relationship/', {
        name: name,
        type: nodeType,
        otherName: otherName,
        otherType: otherType,
        relationshipType: relationshipType
      });

      setMessage(`Node created with name: ${response.data.name}`); 
      setName('');
      setNodeType('');
      setOtherName('');
      setOtherType('');
      setRelationshipType('');

    } catch (error: any) {
      setMessage(error.message);  
    }
  };

  return (
    <Box>
      <Heading mb={4}>Create Node with Relationship</Heading>
      <form onSubmit={handleSubmit}>
        <FormControl mb={2}>
          <FormLabel>Name</FormLabel>
          <Input 
            type="text" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            required 
          />
        </FormControl>
        <FormControl mt={4}>
        <FormLabel>Type</FormLabel>
        <Select value={nodeType} onChange={(e) => setNodeType(e.target.value)}>
          {NODE_TYPES.map((type) => (
            <option key={type} value={type}>
                {type}
            </option>
          ))}
        </Select>
      </FormControl>
        <FormControl mb={2}>
          <FormLabel>Other Name</FormLabel>
          <Input 
            type="text" 
            value={otherName} 
            onChange={(e) => setOtherName(e.target.value)} 
            required 
          />
        </FormControl>
        <FormControl mt={4}>
          <FormLabel>Other Type</FormLabel>
          <Select value={nodeType} onChange={(e) => setOtherType(e.target.value)}>
          {NODE_TYPES.map((type) => (
            <option key={type} value={type}>
                {type}
            </option>
          ))}
        </Select>
        </FormControl>
        
        <FormControl mb={2}>
          <FormLabel>Relationship</FormLabel>
          <Select value={relationshipType} onChange={(e) => setRelationshipType(e.target.value)}>
            {RELATIONSHIPS.map((rel) => (
              <option key={rel} value={rel}> 
                {rel} 
              </option>
            ))}
          </Select>
        </FormControl>
        <Button type="submit">Create Node with Relationship</Button>
        {message && <Box mt={2}>{message}</Box>}
      </form>
    </Box>
  );
};

export default CreateNodeWithRelationshipForm;
