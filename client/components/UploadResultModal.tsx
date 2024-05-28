import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Button,
    Text,
    Box,
    UnorderedList,
    ListItem,
  } from '@chakra-ui/react';
  
  interface UploadResultModalProps {
    isOpen: boolean;
    onClose: () => void;
    uploadResponse: any;
  }
  
  const renderUnimportedRows = (unimported: any) => {
    return Object.keys(unimported).map(sheet => (
      <Box key={sheet} mt={4}>
        <Text fontWeight="bold">Sheet {sheet}:</Text>
        {unimported[sheet].length === 0 ? (
          <Text>No unimported rows</Text>
        ) : (
          <UnorderedList>
            {unimported[sheet].map((row: number) => (
              <ListItem key={row}>Row {row}</ListItem>
            ))}
          </UnorderedList>
        )}
      </Box>
    ));
  };
  
  const UploadResultModal: React.FC<UploadResultModalProps> = ({ isOpen, onClose, uploadResponse }) => (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Upload Result</ModalHeader>
        <ModalBody>
          {uploadResponse && (
            <>
              <Text mb={2}>{uploadResponse.success}</Text>
              {renderUnimportedRows(uploadResponse.unimported)}
            </>
          )}
        </ModalBody>
        <ModalFooter>
          <Button mr={3} onClick={onClose}>
            Close
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
  
  export default UploadResultModal;
  