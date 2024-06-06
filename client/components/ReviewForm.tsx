import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Textarea, NumberInput, NumberInputField, NumberInputStepper, NumberIncrementStepper, NumberDecrementStepper, useToast } from '@chakra-ui/react';
import { apiPost } from '../utils/api';

interface ReviewFormProps {
    query: string;
    curriculum: string;
    reviewId?: number;
    initialComment?: string;
    initialRating?: number;
    onSubmit?: (review: any) => void;
}

const ReviewForm: React.FC<ReviewFormProps> = ({ query, curriculum, reviewId, initialComment = '', initialRating = 0, onSubmit }) => {
    const [comment, setComment] = useState(initialComment);
    const [rating, setRating] = useState(initialRating);
    const toast = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const path = '/review/';
        try {
            const response = await apiPost(path, {
                comment,
                rating,
                query,
                curriculum,
            });
            if (onSubmit) onSubmit(response);
            toast({
                title: 'Success Submitting Review',
                status: 'success',
                duration: 5000,
                isClosable: true,
            });
            window.location.reload();
        } catch (error) {
            toast({
                title: 'Error Submitting Review',
                status: 'error',
                duration: 5000,
                isClosable: true,
            });
        }
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
                    {reviewId ? 'Update Review' : 'Submit Review'}
                </Button>
            </form>
        </Box>
    );
};

export default ReviewForm;
