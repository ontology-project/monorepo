import { Box, Heading, Text, useBreakpointValue } from '@chakra-ui/react'
import { TERMS } from '../utils/constants'

const Glossary: React.FC = () => {
  const columns = useBreakpointValue({ base: 1, md: 2, lg: 3 })

  return (
    <Box>
      <Heading mt={8} mb={4}>
        Glossary
      </Heading>
      <Box
        display="grid"
        gridTemplateColumns={`repeat(${columns}, 1fr)`}
        gap={4}
      >
        {TERMS.map((term, index) => (
          <Box
            key={index}
            p={4}
            borderWidth="1px"
            borderRadius="md"
            bg="gray.50"
            boxShadow="md"
          >
            <Text fontWeight="bold">{term.key}</Text>
            <Text>{term.value}</Text>
          </Box>
        ))}
      </Box>
    </Box>
  )
}

export default Glossary
