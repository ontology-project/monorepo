import React, { useRef, useState } from 'react';
import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Link,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Spinner,
  Text,
  UnorderedList,
  ListItem
} from '@chakra-ui/react';
import { imageApiPost } from '../../utils/api';
import AuthCheck from '../../components/AuthCheck';
import { EXCEL_TEMPLATE_URL } from '../../utils/constants';

interface UploadExcelProps {}

const UploadExcel: React.FC<UploadExcelProps> = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadResponse, setUploadResponse] = useState<any>(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [isUploaded, setIsUploaded] = useState(false);
  const inputFileRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setFile(files[0]);
      setIsUploaded(false);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (file) {
      setLoading(true);
      try {
        const response = await imageApiPost('api/import-excel', file);
        console.log(response);
        setUploadResponse(response);
        setMessage(`Upload success!`);
        onOpen();
        setIsUploaded(true);
      } catch (error: any) {
        setMessage(error.message);
      } finally {
        setFile(null);
        setMessage('');
        setLoading(false);
        if (inputFileRef.current) {
          inputFileRef.current.value = '';
        }
      }
    }
  };

  const renderUnimportedRows = (unimported: any) => {
    return Object.keys(unimported).map(sheet => (
      <Box key={sheet} mt={4}>
        <Text fontWeight="bold">{sheet}:</Text>
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

  return (
    <AuthCheck>
      <Box padding={10}>
        <Heading mb={4}>Upload Excel File</Heading>
        <Link href={EXCEL_TEMPLATE_URL} mb={4} color="purple">Use the template provided here</Link>
        <form onSubmit={handleSubmit}>
          <FormControl mb={4}>
            <FormLabel>Excel file</FormLabel>
            <Input
              padding={1}
              type="file"
              accept=".xls,.xlsx"
              onChange={handleFileChange}
              required
              ref={inputFileRef}
            />
          </FormControl>
          <Button mt={4} type="submit" disabled={loading || (isUploaded && !file)}>
            {loading ? <Spinner size="sm" /> : 'Submit'}
          </Button>
        </form>
        {message && <Box mt={2}>{message}</Box>}

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
      </Box>
    </AuthCheck>
  );
};

export default UploadExcel;
