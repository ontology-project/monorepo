import { Text, Box, Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay } from "@chakra-ui/react";

const DataModal = ({ isOpen, onClose, data }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Query Results</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {data && data.properties && data.properties.length > 0 ? (
            data.properties.map((property, index) => (
              <Box key={index} mb={4}>
                {Object.entries(property).map(([key, value]) => (
                  <Text key={key}><strong>{key}:</strong> {value}</Text>
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
