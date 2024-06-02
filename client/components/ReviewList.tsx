import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Text, Table, Thead, Tbody, Tr, Th, Td, Button } from '@chakra-ui/react';
import ReviewForm from './ReviewForm';

const ReviewList: React.FC = () => {
    const [reviews, setReviews] = useState([]);
    const [editingReview, setEditingReview] = useState(null);

    useEffect(() => {
        const fetchReviews = async () => {
            try {
                const response = await axios.get('/review/reviews/', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                setReviews(response.data);
            } catch (error) {
                console.error('Error fetching reviews:', error);
            }
        };

        fetchReviews();
    }, []);

    const handleDelete = async (id: number) => {
        try {
            await axios.delete(`/review/reviews/${id}/`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                },
            });
            setReviews(reviews.filter((review) => review.id !== id));
        } catch (error) {
            console.error('Error deleting review:', error);
        }
    };

    const handleEdit = (review) => {
        setEditingReview(review);
    };

    const handleReviewSubmit = (review) => {
        if (editingReview) {
            setReviews(reviews.map(r => r.id === review.id ? review : r));
        } else {
            setReviews([...reviews, review]);
        }
        setEditingReview(null);
    };

    return (
        <Box>
            <Table>
                <Thead>
                    <Tr>
                        <Th>Comment</Th>
                        <Th>Rating</Th>
                        <Th>Query</Th>
                        <Th>Curriculum</Th>
                        <Th>Actions</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {reviews.map((review) => (
                        <Tr key={review.id}>
                            <Td>{review.comment}</Td>
                            <Td>{review.rating}</Td>
                            <Td>{review.query}</Td>
                            <Td>{review.curriculum}</Td>
                            <Td>
                                <Button onClick={() => handleEdit(review)}>Edit</Button>
                                <Button onClick={() => handleDelete(review.id)}>Delete</Button>
                            </Td>
                        </Tr>
                    ))}
                </Tbody>
            </Table>
            {editingReview && (
                <ReviewForm
                    query={editingReview.query}
                    curriculum={editingReview.curriculum}
                    reviewId={editingReview.id}
                    initialComment={editingReview.comment}
                    initialRating={editingReview.rating}
                />
            )}
        </Box>
    );
};

export default ReviewList;
