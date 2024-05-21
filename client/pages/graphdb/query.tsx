import { Box, Button, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import AuthCheck from "../../components/AuthCheck";
import { QUERIES } from "../../utils/constants";


interface QueryPageProps {
}

const QueryPage: React.FC<QueryPageProps> = () => {

    return (
        <AuthCheck>
            <Box padding={10}>
                <Heading mb={4}>Query Page</Heading>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                    {QUERIES.map((query, index) => (
                        <Button key={index} size="lg">
                            <Text noOfLines={3} wordBreak="break-word" whiteSpace="normal">
                                {query}
                            </Text>
                        </Button>
                    ))}
                </SimpleGrid>
            </Box>
        </AuthCheck>
    )
}

export default QueryPage;