import React, { useEffect, useState } from 'react';
import { Box, Button, Text, Stack, useToast, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import axios from 'axios';
import { apiDelete, apiGet } from '../utils/api';

interface Review {
  id: number;
  comment: string;
  rating: number;
  query: string;
  curriculum: string;
  created_at: string;
  updated_at: string;
}

const UserReviews: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const toast = useToast();

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await apiGet('/review/');
        setReviews(response);
      } catch (error) {
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

  const handleDelete = async (id: number) => {
    try {
      await apiDelete(`/review/${id}/`);
      setReviews(reviews.filter(review => review.id !== id));
      toast({
        title: 'Review deleted',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error: any) {
      toast({
        title: 'Error deleting review',
        description: error.message || 'An error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleEdit = (id: number) => {
    // Navigate to the edit review page, you may need to implement this
  };

  return (
    <Box>
      <Text fontSize="2xl" mb={4}>Your Reviews</Text>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Query</Th>
            <Th>Curriculum</Th>
            <Th>Comment</Th>
            <Th>Rating</Th>
            <Th>Created At</Th>
            <Th>Updated At</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {reviews.map(review => (
            <Tr key={review.id}>
              <Td>{review.query}</Td>
              <Td>{review.curriculum}</Td>
              <Td>{review.comment}</Td>
              <Td>{review.rating}</Td>
              <Td>{new Date(review.created_at).toLocaleString()}</Td>
              <Td>{new Date(review.updated_at).toLocaleString()}</Td>
              <Td>
                <Button colorScheme="teal" size="sm" mr={2} onClick={() => handleEdit(review.id)}>
                  Edit
                </Button>
                <Button colorScheme="red" size="sm" onClick={() => handleDelete(review.id)}>
                  Delete
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default UserReviews;
