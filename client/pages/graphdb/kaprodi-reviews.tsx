import React, { useEffect, useState } from 'react';
import { Box, Heading, Table, Tbody, Td, Th, Thead, Tr, useToast } from '@chakra-ui/react';
import { apiGet } from '../../utils/api';
import AuthCheck from '../../components/AuthCheck';
import { useRouter } from 'next/router';
import { formatRelative } from 'date-fns/formatRelative';

interface Review {
  id: number;
  comment: string;
  rating: number;
  query: string;
  curriculum: string;
  created_at: string;
  updated_at: string;
  reviewer: string;
}

const KaprodiReviews: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const toast = useToast();
  const router = useRouter();
  
  useEffect(() => {
    if (localStorage.getItem('isKaprodi') === 'false') {
      router.push('/');
    }
  }, [router]);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await apiGet('/review/');
        setReviews(response);
      } catch (error: any) {
        toast({
          title: 'Error loading reviews',
          description: error.message || 'An error occurred',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    };

    fetchReviews();
  }, []);

  return (
    <AuthCheck>
      <Box padding={10}>
      <Heading mb={4}>Review Comments</Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Curriculum</Th>
            <Th>Query</Th>
            <Th>Comment</Th>
            <Th>Rating</Th>
            <Th>Created At</Th>
            <Th>Updated At</Th>
            <Th>Reviewer</Th>
          </Tr>
        </Thead>
        <Tbody>
          {reviews.map(review => (
            <Tr key={review.id}>
              <Td>{review.curriculum}</Td>
              <Td>{review.query}</Td>
              <Td>{review.comment}</Td>
              <Td>{review.rating}</Td>
              <Td>{formatRelative(review.created_at, new Date())}</Td>
              <Td>{formatRelative(review.updated_at, new Date())}</Td>
              <Td>{review.reviewer}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
    </AuthCheck>
  );
};

export default KaprodiReviews;