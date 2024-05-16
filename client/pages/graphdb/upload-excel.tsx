import React, { useState } from 'react';
import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Link,
} from '@chakra-ui/react';
import { imageApiPost } from '../../utils/api';
import AuthCheck from '../../components/AuthCheck';
import { EXCEL_TEMPLATE_URL } from '../../utils/constants';

interface UploadExcelProps {}

const UploadExcel: React.FC<UploadExcelProps> = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setFile(files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (file) {
      console.log('Uploading file:', file.name);

      try {
        const response = await imageApiPost('api/import-excel', file);
        console.log(response);
        setMessage(`Upload success!\nResponse: ${JSON.stringify(response)}`);
      } catch (error: any) {
        setMessage(error.message);
      }
    }
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
            />
          </FormControl>
          <Button mt={4} type="submit">
            Submit
          </Button>
        </form>
        {message && <Box mt={2}>{message}</Box>}
      </Box>
    </AuthCheck>

  );
};

export default UploadExcel;
