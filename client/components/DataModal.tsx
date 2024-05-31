import { Text, Box, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from "@chakra-ui/react";
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
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Query Results</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Text mb={4}>{data?.success}</Text>
          {data && data.properties && data.properties.length > 0 ? (
            data.properties.map((property, index) => (
              <Box key={index} mb={4}>
                {Object.entries(property).map(([key, value]) => (
                  <Text key={key}><strong>{getDisplayKey(key)}:</strong> {getDisplayValue(value)}</Text>
                ))}
              </Box>
            ))
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
