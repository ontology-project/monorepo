import React, { useEffect, useState } from 'react';
import {
  Box,
  Heading,
  Table,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  useToast,
  Select,
  Button,
  Input,
} from '@chakra-ui/react';
import { apiGet } from '../../utils/api';
import AuthCheck from '../../components/AuthCheck';
import { useRouter } from 'next/router';
import { formatRelative } from 'date-fns';
import { TOAST_DURATION } from '../../utils/constants';

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
  const [sortedReviews, setSortedReviews] = useState<Review[]>([]);
  const [visibleReviewers, setVisibleReviewers] = useState<string[]>([]);
  const [curriculumOptions, setCurriculumOptions] = useState<string[]>([]);
  const [curriculumFilters, setCurriculumFilters] = useState<{ [key: string]: string }>({});
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
        const sorted = response.sort((a: Review, b: Review) => {
          if (a.curriculum < b.curriculum) return -1;
          if (a.curriculum > b.curriculum) return 1;
          if (a.query < b.query) return -1;
          if (a.query > b.query) return 1;
          return 0;
        });
        setReviews(sorted);
        setSortedReviews(sorted);
        setVisibleReviewers([...new Set(sorted.map((review: Review) => review.reviewer))]);
      } catch (error: any) {
        toast({
          title: 'Error loading reviews',
          description: error.message || 'An error occurred',
          status: 'error',
          duration: TOAST_DURATION,
          isClosable: true,
        });
      }
    };

    fetchReviews();
  }, [toast]);

  useEffect(() => {
    const fetchCurriculums = async () => {
      try {
        const data = await apiGet('api/graphdb/get-curriculums');
        setCurriculumOptions(data.curriculums);
      } catch (error: any) {
        console.log("error fetching curriculums", error)
      }
    };

    fetchCurriculums();
  }, []);

  const handleFilterChange = (reviewer: string, e: React.ChangeEvent<HTMLSelectElement>) => {
    setCurriculumFilters({
      ...curriculumFilters,
      [reviewer]: e.target.value,
    });
  };

  const toggleReviewerVisibility = (reviewer: string) => {
    setVisibleReviewers(prev => 
      prev.includes(reviewer) 
        ? prev.filter(r => r !== reviewer) 
        : [...prev, reviewer]
    );
  };

  const getFilteredReviews = (reviewer: string) => {
    if (!curriculumFilters[reviewer]) return groupedReviews[reviewer];
    return groupedReviews[reviewer].filter(review => review.curriculum === curriculumFilters[reviewer]);
  };

  // Group reviews by reviewer
  const groupedReviews = sortedReviews.reduce((acc: { [key: string]: Review[] }, review) => {
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
            <Box display="flex" alignItems="center" justifyContent="space-between" mb={4}>
              <Heading
                size="md"
                onClick={() => toggleReviewerVisibility(reviewer)}
                cursor="pointer"
                _hover={{ textDecoration: 'underline' }}
                flex="1"
              >
                {reviewer} ({visibleReviewers.includes(reviewer) ? 'Hide' : 'Show'})
              </Heading>
              {visibleReviewers.includes(reviewer) && (
                <Select
                  placeholder="All Curriculums"
                  value={curriculumFilters[reviewer] || ''}
                  onChange={(e) => handleFilterChange(reviewer, e)}
                  size="sm"
                  ml={4}
                  flex="1"
                >
                  {curriculumOptions.map((curriculum) => (
                    <option key={curriculum} value={curriculum}>
                      {curriculum}
                    </option>
                  ))}
                </Select>
              )}
            </Box>
            {visibleReviewers.includes(reviewer) && (
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
                  {getFilteredReviews(reviewer).map(review => (
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
            )}
          </Box>
        ))}
      </Box>
    </AuthCheck>
  );

};

export default KaprodiReviews;
