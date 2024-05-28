import React, { useEffect, useState } from 'react';
import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Link,
  Spinner,
  Text
} from '@chakra-ui/react';
import AuthCheck from '../../components/AuthCheck';
import { EXCEL_TEMPLATE_URL } from '../../utils/constants';
import UploadResultModal from '../../components/UploadResultModal';
import { useFileUpload } from '../../utils/util';
import { useRouter } from 'next/router';


const UploadExcel: React.FC = () => {
  const {
    file,
    message,
    loading,
    uploadResponse,
    isUploaded,
    inputFileRef,
    handleFileChange,
    handleSubmit,
    setUploadResponse,
  } = useFileUpload();
  const router = useRouter();

  useEffect(() => {
    if (localStorage.getItem('isKaprodi') === 'false') {
      router.push('/');
    }
  }, [router]);

  return (
    <AuthCheck>
      <Box padding={10}>
        <Heading mb={4}>Curriculum File Upload</Heading>
        <Link href={EXCEL_TEMPLATE_URL} mb={4} color="purple" target="_blank">
          Download the template provided here
        </Link>
        <form onSubmit={handleSubmit}>
          <FormControl mb={4}>
            <FormLabel>Excel file upload</FormLabel>
            <Input
              padding={1}
              type="file"
              accept=".xls,.xlsx"
              onChange={handleFileChange}
              required
              ref={inputFileRef}
            />
          </FormControl>
          <Button type="submit" disabled={loading || (isUploaded && !file)}>
            {loading ? <Spinner size="sm" /> : 'Submit'}
          </Button>
        </form>
        {message && <Box mt={2}>{message}</Box>}

        <UploadResultModal
          isOpen={!!uploadResponse}
          onClose={() => uploadResponse && setUploadResponse(null)}
          uploadResponse={uploadResponse}
        />
      </Box>
    </AuthCheck>
  );
};

export default UploadExcel;
