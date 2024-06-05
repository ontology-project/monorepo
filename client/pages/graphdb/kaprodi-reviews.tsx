import React, { useEffect, useState } from 'react';
import { Box, Heading, Table, Tbody, Td, Th, Thead, Tr, useToast } from '@chakra-ui/react';
import { apiGet } from '../../utils/api';
import AuthCheck from '../../components/AuthCheck';
import { useRouter } from 'next/router';
import { formatRelative } from 'date-fns';

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

  // Group reviews by reviewer
  const groupedReviews = reviews.reduce((acc: { [key: string]: Review[] }, review) => {
    acc[review.reviewer] = acc[review.reviewer] || [];
    acc[review.reviewer].push(review);
    return acc;
  }, {});

  return (
    <AuthCheck>
      <Box padding={10}>
        <Heading mb={4}>Review Comments</Heading>
        {Object.keys(groupedReviews).map(reviewer => (
          <Box key={reviewer} mb={8}>
            <Heading size="md" mb={4}>{reviewer}</Heading>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Curriculum</Th>
                  <Th>Query</Th>
                  <Th>Comment</Th>
                  <Th>Rating</Th>
                  <Th>Created At</Th>
                  <Th>Updated At</Th>
                </Tr>
              </Thead>
              <Tbody>
                {groupedReviews[reviewer].map(review => (
                  <Tr key={review.id}>
                    <Td>{review.curriculum}</Td>
                    <Td>{review.query}</Td>
                    <Td>{review.comment}</Td>
                    <Td>{review.rating}</Td>
                    <Td>{formatRelative(new Date(review.created_at), new Date())}</Td>
                    <Td>{formatRelative(new Date(review.updated_at), new Date())}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        ))}
      </Box>
    </AuthCheck>
  );
};

export default KaprodiReviews;
