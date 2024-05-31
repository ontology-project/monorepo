import { Text, Box, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";
import { QueryApiResponse } from "../utils/types";
import { keyMappings, valueMappings } from "../utils/keyMappings";

interface DataModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: QueryApiResponse | null;
}

const DataModal: React.FC<DataModalProps> = ({ isOpen, onClose, data }) => {
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
          <Button mr={3} onClick={onClose}>Close</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default DataModal;
