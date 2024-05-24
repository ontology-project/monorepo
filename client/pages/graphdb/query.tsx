import { Box, Button, Heading, Select, SimpleGrid, Text, useDisclosure } from "@chakra-ui/react";
import AuthCheck from "../../components/AuthCheck";
import { QUERIES } from "../../utils/constants";
import { apiGet } from "../../utils/api";
import { useEffect, useState } from "react";
import DataModal from "../../components/DataModal";


interface QueryPageProps {
}

const QueryPage: React.FC<QueryPageProps> = () => {
    const [curriculumOptions, setCurriculumOptions] = useState<string[]>();
    const [curriculum, setCurriculum] = useState<string>();
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [modalData, setModalData] = useState(null);

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

    const handleButtonClick = async (endpoint: string) => {
        try {
          const data = await apiGet(endpoint, { curriculum: curriculum });
          setModalData(data);
          onOpen();
        } catch (error: any) {
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
                        <Button key={index} size="lg" padding={8} onClick={() => handleButtonClick(query.endpoint)}>
                            <Text noOfLines={3} wordBreak="break-word" whiteSpace="normal">
                                {query.text}
                            </Text>
                        </Button>
                    ))}
                </SimpleGrid>
            </Box>
            <DataModal isOpen={isOpen} onClose={onClose} data={modalData} />
        </AuthCheck>
    )
}

export default QueryPage;