import { Text, Box, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Table, Thead, Tbody, Tr, Th, Td, Flex } from "@chakra-ui/react";
import { QueryApiResponse } from "../utils/types";
import { keyMappings, valueMappings } from "../utils/keyMappings";
import ReviewForm from "./ReviewForm";

interface DataModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: QueryApiResponse | null;
  query: string;
  curriculum: string;
}

const DataModal: React.FC<DataModalProps> = ({ isOpen, onClose, data, query, curriculum }) => {
  const getDisplayKey = (key: string) => {
    return keyMappings[key] || key;
  };

  const getDisplayValue = (value: string) => {
    return valueMappings[value] || value;
  };
  
  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Query Results</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Text mb={4}>{data?.success}</Text>
          {data && data.properties && data.properties.length > 0 ? (
            <Box overflowX="auto">
              <Table variant="simple">
                <Thead>
                  <Tr>
                    {Object.keys(data.properties[0]).map((key) => (
                      <Th key={key}>{getDisplayKey(key)}</Th>
                    ))}
                  </Tr>
                </Thead>
                <Tbody>
                  {data.properties.map((property, index) => (
                    <Tr key={index}>
                      {Object.entries(property).map(([key, value]) => (
                        <Td key={key}>{getDisplayValue(value)}</Td>
                      ))}
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </Box>
          ) : (
            <Text>No properties found.</Text>
          )}
        </ModalBody>
        <ModalFooter>
          <Flex w="full" align="center">
            <Box flex="1" mr={4}>
              <ReviewForm query={query} curriculum={curriculum} />
            </Box>
            <Button onClick={onClose}>Close</Button>
          </Flex>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default DataModal;
