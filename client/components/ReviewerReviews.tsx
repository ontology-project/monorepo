import React, { useEffect, useState } from 'react';
import { Box, Button, Text, Table, Tbody, Td, Th, Thead, Tr, useToast, Input, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper } from '@chakra-ui/react';
import { apiDelete, apiGet, apiPut } from '../utils/api';
import { formatRelative } from 'date-fns/formatRelative';

interface Review {
  id: number;
  comment: string;
  rating: number;
  query: string;
  curriculum: string;
  created_at: string;
  updated_at: string;
}

const ReviewerReviews: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [editableReviewId, setEditableReviewId] = useState<number | null>(null);
  const [editedComment, setEditedComment] = useState<string>('');
  const [editedRating, setEditedRating] = useState<number>(0);
  const toast = useToast();

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

  const handleEdit = (review: Review) => {
    setEditableReviewId(review.id);
    setEditedComment(review.comment);
    setEditedRating(review.rating);
  };

  const handleCancelEdit = () => {
    setEditableReviewId(null);
  };

  const handleSave = async (id: number) => {
    try {
      const review = reviews.find(review => review.id === id);
      if (!review) return;
      
      const updatedReview = { comment: editedComment, rating: editedRating, query: review.query, curriculum: review.curriculum };
      await apiPut(`/review/${id}/`, updatedReview);
      setReviews(reviews.map(review => review.id === id ? { ...review, ...updatedReview } : review));
      setEditableReviewId(null);
      toast({
        title: 'Review updated',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error: any) {
      toast({
        title: 'Error updating review',
        description: error.message || 'An error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Curriculum</Th>
            <Th>Query</Th>
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
              <Td>{review.curriculum}</Td>
              <Td>{review.query}</Td>
              <Td>
                {editableReviewId === review.id ? (
                  <Input
                    value={editedComment}
                    onChange={(e) => setEditedComment(e.target.value)}
                  />
                ) : (
                  review.comment
                )}
              </Td>
              <Td>
                {editableReviewId === review.id ? (
                  <NumberInput
                    min={0}
                    max={4}
                    value={editedRating}
                    onChange={(valueString) => setEditedRating(parseInt(valueString))}
                  >
                    <NumberInputField />
                    <NumberInputStepper>
                      <NumberIncrementStepper />
                      <NumberDecrementStepper />
                    </NumberInputStepper>
                  </NumberInput>
                ) : (
                  review.rating
                )}
              </Td>
              <Td>{formatRelative(review.created_at, new Date())}</Td>
              <Td>{formatRelative(review.updated_at, new Date())}</Td>
              <Td>
                {editableReviewId === review.id ? (
                  <>
                    <Button colorScheme="teal" size="sm" mr={2} mb={2} onClick={() => handleSave(review.id)}>
                      Submit
                    </Button>
                    <Button colorScheme="gray" size="sm" onClick={handleCancelEdit}>
                      Cancel
                    </Button>
                  </>
                ) : (
                  <>
                    <Button colorScheme="teal" size="sm" mr={2} my={1} onClick={() => handleEdit(review)}>
                      Edit
                    </Button>
                    <Button colorScheme="red" size="sm" my={1} onClick={() => handleDelete(review.id)}>
                      Delete
                    </Button>
                  </>
                )}
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default ReviewerReviews;
