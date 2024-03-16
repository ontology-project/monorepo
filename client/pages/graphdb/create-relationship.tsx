import React, { useEffect, useState } from 'react';
import { Box, Heading, FormControl, FormLabel, Input, Button, Select } from '@chakra-ui/react';
import { apiGet, apiPost } from '../../utils/api';

interface CreateNodeWithRelationshipFormProps {}


const CreateNodeWithRelationshipForm: React.FC<CreateNodeWithRelationshipFormProps> = () => {
  const [name, setName] = useState('');
  const [nodeType, setNodeType] = useState('');
  const [rightName, setOtherName] = useState('');
  const [rightType, setOtherType] = useState('');
  const [relationshipType, setRelationshipType] = useState('');
  const [message, setMessage] = useState('');
  const [nodeTypeOptions, setNodeTypeOptions] = useState<string[]>();
  const [objectProperties, setObjectProperties] = useState<string[]>()

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const data = await apiGet('api/graphdb/get-classes');
        setNodeTypeOptions(data.classes);  
      } catch (error: any) { 
        setMessage(error.message || 'Error fetching classes.'); 
      }
    };
  
    fetchClasses();
  }, []);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const data = await apiGet('api/graphdb/get-object-properties');
        setObjectProperties(data.properties);  
      } catch (error: any) { 
        setMessage(error.message || 'Error fetching classes.'); 
      }
    };
  
    fetchProperties();
  }, []);


  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await apiPost('api/graphdb/create-relationship/', {
        name: name,
        type: nodeType,
        rightName: rightName,
        rightType: rightType,
        relationshipType: relationshipType
      });

      

      setMessage(`${name}-${relationshipType}-${rightName} created.`); 
      setName('');
      setNodeType('');
      setOtherName('');
      setOtherType('');
      setRelationshipType('');

    } catch (error: any) {
      setMessage(error.message);  
    }
  };

  if (!nodeTypeOptions || !objectProperties) {
    return null;
  }

  return (
    <Box padding={10}>
      <Heading mb={4}>GraphDB Create Node with Relationship</Heading>
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
          {nodeTypeOptions.map((type) => (
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
            value={rightName} 
            onChange={(e) => setOtherName(e.target.value)} 
            required 
          />
        </FormControl>
        <FormControl mt={4}>
          <FormLabel>Other Type</FormLabel>
          <Select value={rightType} onChange={(e) => setOtherType(e.target.value)}>
          {nodeTypeOptions.map((type) => (
            <option key={type} value={type}>
                {type}
            </option>
          ))}
        </Select>
        </FormControl>
        
        <FormControl mt={4}>
          <FormLabel>Relationship</FormLabel>
          <Select value={relationshipType} onChange={(e) => setRelationshipType(e.target.value)}>
            {objectProperties.map((rel) => (
              <option key={rel} value={rel}> 
                {rel} 
              </option>
            ))}
          </Select>
        </FormControl>
        <Button mt={4} type="submit">Create Node with Relationship</Button>
        {message && <Box mt={2}>{message}</Box>}
      </form>
    </Box>
  );
};

export default CreateNodeWithRelationshipForm;
