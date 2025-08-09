import { Grid, Card, Text, Group, Stack, Badge, ActionIcon, Progress, LoadingOverlay, Button } from '@mantine/core'
import { IconEye, IconTrendingUp, IconSparkles, IconFileText, IconBuildingStore, IconCalendar } from '@tabler/icons-react'
import { useQuery } from '@tanstack/react-query'
import { contentApi, businessApi } from '../lib/api'
import { useNavigate } from 'react-router-dom'
import { useMemo } from 'react'

interface Content {
  id: number
  title: string
  content_text: string
  content_type: string
  status: string
  seo_score?: number
  created_at: string
  business?: {
    id: number
    name: string
    industry?: string
  }
  keywords?: string[]
  meta_description?: string
}


const contentTypeLabels = {
  blog_post: 'Blog Post',
  linkedin_post: 'LinkedIn',
  twitter_post: 'Twitter',
  facebook_post: 'Facebook',
  instagram_post: 'Instagram',
  email: 'Email'
}

const statusColors = {
  published: 'green',
  pending_approval: 'yellow',
  draft: 'gray',
  rejected: 'red'
}

export function Dashboard() {
  const navigate = useNavigate()
  
  // Fetch content and businesses
  const { data: content = [], isLoading: contentLoading } = useQuery({
    queryKey: ['content'],
    queryFn: () => contentApi.list().then((res: any) => res.data),
  })

  const { data: businesses = [], isLoading: businessesLoading } = useQuery({
    queryKey: ['businesses'],
    queryFn: () => businessApi.list().then((res: any) => res.data),
  })

  // Calculate dashboard metrics
  const dashboardStats = useMemo(() => {
    const totalContent = content.length
    const publishedContent = content.filter((item: Content) => item.status === 'published').length
    const pendingContent = content.filter((item: Content) => item.status === 'pending_approval').length
    const avgSeoScore = content.length > 0 
      ? Math.round(content.reduce((sum: number, item: Content) => sum + (item.seo_score || 0), 0) / content.length)
      : 0
    
    // Recent content (last 7 days)
    const oneWeekAgo = new Date()
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
    const recentContent = content.filter((item: Content) => new Date(item.created_at) > oneWeekAgo)
    
    // Content by type
    const contentByType = content.reduce((acc: Record<string, number>, item: Content) => {
      acc[item.content_type] = (acc[item.content_type] || 0) + 1
      return acc
    }, {})

    return {
      totalContent,
      publishedContent,
      pendingContent,
      avgSeoScore,
      recentContent: recentContent.length,
      contentByType,
      activeBusinesses: businesses.length
    }
  }, [content, businesses])

  const recentContentItems = useMemo(() => {
    return content
      .sort((a: Content, b: Content) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 5)
  }, [content])

  const isLoading = contentLoading || businessesLoading
  return (
    <Stack gap="lg">
      <LoadingOverlay visible={isLoading} />
      
      <Group justify="space-between">
        <Text size="xl" fw={700}>
          Dashboard Overview
        </Text>
        <Group>
          <Button 
            leftSection={<IconSparkles size={16} />}
            onClick={() => navigate('/generate')}
            variant="filled"
          >
            Generate Content
          </Button>
          <Badge size="lg" variant="light" color="green">
            AI Active
          </Badge>
        </Group>
      </Group>

      <Grid>
        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Total Content
              </Text>
              <IconFileText size={16} color="blue" />
            </Group>
            <Text fw={700} size="xl">
              {dashboardStats.totalContent}
            </Text>
            <Text size="xs" c="dimmed">
              {dashboardStats.recentContent} created this week
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Published
              </Text>
              <IconEye size={16} color="green" />
            </Group>
            <Text fw={700} size="xl">
              {dashboardStats.publishedContent}
            </Text>
            <Text size="xs" c="dimmed">
              Content live and active
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Avg SEO Score
              </Text>
              <IconTrendingUp size={16} color="orange" />
            </Group>
            <Text fw={700} size="xl">
              {dashboardStats.avgSeoScore}%
            </Text>
            <Text size="xs" c="dimmed">
              Across all content
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Active Businesses
              </Text>
              <IconBuildingStore size={16} color="violet" />
            </Group>
            <Text fw={700} size="xl">
              {dashboardStats.activeBusinesses}
            </Text>
            <Text size="xs" c="dimmed">
              All configured
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 8 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h={380}>
            <Group justify="space-between" mb="md">
              <Text fw={600}>Recent Content</Text>
              <Button 
                variant="subtle" 
                size="xs"
                onClick={() => navigate('/content')}
              >
                View All
              </Button>
            </Group>
            <Stack gap="md" style={{ overflowY: 'auto', maxHeight: '300px' }}>
              {recentContentItems.length > 0 ? (
                recentContentItems.map((item: Content) => (
                  <div key={item.id}>
                    <Group justify="space-between" mb={5}>
                      <div style={{ flex: 1 }}>
                        <Text size="sm" fw={500} style={{ 
                          overflow: 'hidden', 
                          textOverflow: 'ellipsis', 
                          whiteSpace: 'nowrap',
                          maxWidth: '300px'
                        }}>
                          {item.title}
                        </Text>
                        <Group gap="xs">
                          <Badge size="xs" variant="light">
                            {contentTypeLabels[item.content_type as keyof typeof contentTypeLabels]}
                          </Badge>
                          <Badge size="xs" color={statusColors[item.status as keyof typeof statusColors]}>
                            {item.status.replace('_', ' ')}
                          </Badge>
                        </Group>
                      </div>
                      <Text size="sm" c="dimmed">
                        {item.seo_score ? `${item.seo_score}% SEO` : 'No Score'}
                      </Text>
                    </Group>
                    <Progress 
                      value={item.seo_score || 0} 
                      color={
                        (item.seo_score || 0) >= 80 ? 'green' : 
                        (item.seo_score || 0) >= 60 ? 'blue' : 
                        (item.seo_score || 0) >= 40 ? 'yellow' : 'red'
                      } 
                      size="sm" 
                    />
                  </div>
                ))
              ) : (
                <Text ta="center" c="dimmed" py="xl">
                  No content created yet. Start by generating your first piece of content!
                </Text>
              )}
            </Stack>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 4 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h={380}>
            <Text fw={600} mb="md">
              Quick Actions
            </Text>
            <Stack gap="sm">
              <Card 
                shadow="xs" 
                padding="sm" 
                radius="sm" 
                withBorder 
                style={{ cursor: 'pointer' }}
                onClick={() => navigate('/generate')}
              >
                <Group>
                  <ActionIcon variant="light" color="blue" size="lg">
                    <IconSparkles size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Generate Content</Text>
                    <Text size="xs" c="dimmed">Create new AI content</Text>
                  </div>
                </Group>
              </Card>
              
              <Card 
                shadow="xs" 
                padding="sm" 
                radius="sm" 
                withBorder 
                style={{ cursor: 'pointer' }}
                onClick={() => navigate('/content')}
              >
                <Group>
                  <ActionIcon variant="light" color="green" size="lg">
                    <IconFileText size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Review Content</Text>
                    <Text size="xs" c="dimmed">
                      {dashboardStats.pendingContent} items pending approval
                    </Text>
                  </div>
                </Group>
              </Card>
              
              <Card 
                shadow="xs" 
                padding="sm" 
                radius="sm" 
                withBorder 
                style={{ cursor: 'pointer' }}
                onClick={() => navigate('/businesses')}
              >
                <Group>
                  <ActionIcon variant="light" color="violet" size="lg">
                    <IconBuildingStore size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Manage Businesses</Text>
                    <Text size="xs" c="dimmed">
                      {dashboardStats.activeBusinesses} businesses configured
                    </Text>
                  </div>
                </Group>
              </Card>
              
              <Card 
                shadow="xs" 
                padding="sm" 
                radius="sm" 
                withBorder 
                style={{ cursor: 'not-allowed', opacity: 0.8 }}
              >
                <Group>
                  <ActionIcon variant="light" color="orange" size="lg">
                    <IconCalendar size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Schedule Posts</Text>
                    <Text size="xs" c="dimmed">Coming soon</Text>
                  </div>
                </Group>
              </Card>
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>
    </Stack>
  )
}