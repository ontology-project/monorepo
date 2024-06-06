import { Box, Button, Heading, Select, SimpleGrid, Text, useDisclosure, useToast } from "@chakra-ui/react";
import AuthCheck from "../../components/AuthCheck";
import { QUERIES } from "../../utils/constants";
import { apiGet } from "../../utils/api";
import { useEffect, useState } from "react";
import DataModal from "../../components/DataModal";
import { QueryApiResponse } from "../../utils/types";
import { useRouter } from "next/router";
import ReviewerReviews from "../../components/ReviewerReviews";
import Glossary from "../../components/Glossary";


interface QueryPageProps {
}

const QueryPage: React.FC<QueryPageProps> = () => {
    const [curriculumOptions, setCurriculumOptions] = useState<string[]>();
    const [curriculum, setCurriculum] = useState<string>("");
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [modalData, setModalData] = useState<QueryApiResponse | null>(null);
    const router = useRouter();
    const [query, setQuery] = useState<string>("");
    const toast = useToast();

    useEffect(() => {
        if (localStorage.getItem('isKaprodi') === 'true') {
        router.push('/');
        }
    }, [router]);

    useEffect(() => {
        const fetchCurriculums = async () => {
          try {
            const data = await apiGet('api/graphdb/get-curriculums');
            setCurriculumOptions(data.curriculums); 
            if (data.curriculums.length > 0) {
                setCurriculum(data.curriculums[0]);
            } 
          } catch (error: any) {
            console.log("error fetching curriculums", error)
          }
        };
      
        fetchCurriculums();
      }, []);

    const handleButtonClick = async (query: any) => {
        try {
          const data: QueryApiResponse = await apiGet(query.endpoint, { curriculum: curriculum });
          setModalData(data);
          setQuery(query.text)
          onOpen();
          toast({
            title: data.success,
            status: 'success',
            duration: 5000,
            isClosable: true,
          });
        } catch (error: any) {
            console.log("error", error)
        }
      };

    if (!curriculumOptions) {
        return null;
    }

    return (
        <AuthCheck>
            <Box padding={10}>
                <Heading mb={4}>Queries for Curriculum Review</Heading>
                <Text>Select Curriculum</Text>
                <Select mb={4} value={curriculum} onChange={(e) => setCurriculum(e.target.value)}>
                    {curriculumOptions.map((curr) => (
                        <option key={curr} value={curr}>
                            {curr}
                        </option>
                    ))}
                </Select>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                    {QUERIES.map((query, index) => (
                        <Button key={index} size="lg" padding={8} onClick={() => handleButtonClick(query)}>
                            <Text noOfLines={3} wordBreak="break-word" whiteSpace="normal">
                                {query.text}
                            </Text>
                        </Button>
                    ))}
                </SimpleGrid>
                <ReviewerReviews></ReviewerReviews>
                <Glossary></Glossary>
            </Box>
            <DataModal isOpen={isOpen} onClose={onClose} data={modalData} query={query} curriculum={curriculum} />
        </AuthCheck>
    )
}

export default QueryPage;