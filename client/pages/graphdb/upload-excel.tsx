import React, { useState } from 'react';
import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
} from '@chakra-ui/react';

interface UploadExcelProps {}

const UploadExcel: React.FC<UploadExcelProps> = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setFile(files[0]);
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (file) {
      console.log("Uploading file:", file.name);
    }
  };

  return (
    <Box padding={10}>
      <Heading mb={4}>Upload Excel File</Heading>
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
    </Box>
  );
};

export default UploadExcel;
