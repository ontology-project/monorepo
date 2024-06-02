import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Textarea, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper } from '@chakra-ui/react';

interface ReviewFormProps {
  query: string;
  curriculum: string;
  onSubmit: (review: { query: string; curriculum: string; comment: string; rating: number }) => void;
}

const ReviewForm: React.FC<ReviewFormProps> = ({ query, curriculum, onSubmit }) => {
  const [comment, setComment] = useState('');
  const [rating, setRating] = useState(0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ query, curriculum, comment, rating });
  };

  return (
    <Box borderWidth="1px" borderRadius="lg" p={4}>
      <form onSubmit={handleSubmit}>
        <FormControl id="comment" mb={2}>
          <FormLabel fontSize="sm">Review</FormLabel>
          <Textarea
            placeholder="Write your review here..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
        </FormControl>

        <FormControl id="rating" mb={2}>
          <FormLabel fontSize="sm">Rating</FormLabel>
          <NumberInput
            min={0}
            max={4}
            value={rating}
            onChange={(valueString) => setRating(parseInt(valueString))}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        </FormControl>

        <Button type="submit" width="full" mt={2}>
          Submit Review
        </Button>
      </form>
    </Box>
  );
};

export default ReviewForm;
