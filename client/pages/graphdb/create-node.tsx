import React, { useEffect, useState } from 'react'
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
  Text,
} from '@chakra-ui/react'
import { apiGet, apiPost } from '../../utils/api'

interface CreateNodeProps {}

const CreateNode: React.FC<CreateNodeProps> = () => {
  const [nodeName, setNodeName] = useState('')
  const [nodeType, setNodeType] = useState('')
  const [message, setMessage] = useState('')
  const [nodeTypeOptions, setNodeTypeOptions] = useState<string[]>()

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const data = await apiGet('api/graphdb/get-classes')
        setNodeTypeOptions(data.classes)
      } catch (error: any) {
        setMessage(error.message || 'Error fetching classes.')
      }
    }

    fetchClasses()
  }, [])

  const handleSubmit = async () => {
    try {
      const data = await apiPost('api/graphdb/create-node/', {
        name: nodeName,
        type: nodeType,
      })

      setMessage(`${nodeType} created with name: ${nodeName}`)
      setNodeName('')
    } catch (error: any) {
      setMessage(error.message)
    }
  }

  if (!nodeTypeOptions) {
    return null
  }

  return (
    <Box padding={10}>
      <Heading mb={4}>GraphDB Create Node</Heading>
      <FormControl mt={4}>
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
          {nodeTypeOptions.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </Select>
      </FormControl>
      <Button onClick={handleSubmit} mt={4} type="submit">
        Create Node
      </Button>
      {message && <Text>{message}</Text>}
    </Box>
  )
}

export default CreateNode
