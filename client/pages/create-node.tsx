import React, { useState } from 'react';
import { NODE_TYPES } from '../utils/constants';
import { Box, Button, FormControl, FormLabel, Heading, Input, Select, Text } from '@chakra-ui/react';
import { apiPost } from '../utils/api';

interface CreateNodeFormProps {}

const CreateNodeForm: React.FC<CreateNodeFormProps> = () => {
  const [nodeName, setNodeName] = useState('');
  const [nodeType, setNodeType] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    try {
      const data = await apiPost('api/create-node/', {
        name: nodeName,
        type: nodeType
      });

      setMessage(`${data.type} created with name: ${data.name}`); 
      setNodeName('');

    } catch (error: any) {
      setMessage(error.message);
    }
  };

  return (
    <Box>
      <Heading fontSize='5xl'>Create Node</Heading>
      <FormControl>
        <FormLabel>Name</FormLabel>
        <Input 
          type="text" 
          placeholder="Enter node name"
          value={nodeName} 
          onChange={(e) => setNodeName(e.target.value)} 
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
      <Button onClick={handleSubmit} mt={4} type="submit">Create Node</Button>
      {message && <Text>{message}</Text>} 
    </Box>
  );
};

export default CreateNodeForm;
