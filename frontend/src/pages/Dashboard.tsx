import { Grid, Card, Text, Group, Stack, Badge, ActionIcon, Progress } from '@mantine/core'
import { IconEye, IconThumbUp, IconShare, IconTrendingUp } from '@tabler/icons-react'

export function Dashboard() {
  return (
    <Stack gap="lg">
      <Group justify="space-between">
        <Text size="xl" fw={700}>
          Dashboard Overview
        </Text>
        <Badge size="lg" variant="light" color="green">
          AI Active
        </Badge>
      </Group>

      <Grid>
        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Content Generated
              </Text>
              <IconTrendingUp size={16} color="green" />
            </Group>
            <Text fw={700} size="xl">
              24
            </Text>
            <Text size="xs" c="dimmed">
              +12% from last week
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Total Views
              </Text>
              <IconEye size={16} color="blue" />
            </Group>
            <Text fw={700} size="xl">
              1,247
            </Text>
            <Text size="xs" c="dimmed">
              +8% from last week
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Engagement
              </Text>
              <IconThumbUp size={16} color="orange" />
            </Group>
            <Text fw={700} size="xl">
              89%
            </Text>
            <Text size="xs" c="dimmed">
              +5% from last week
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder>
            <Group justify="space-between" mb="xs">
              <Text size="sm" c="dimmed" fw={500}>
                Active Businesses
              </Text>
              <IconShare size={16} color="violet" />
            </Group>
            <Text fw={700} size="xl">
              3
            </Text>
            <Text size="xs" c="dimmed">
              All configured
            </Text>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 8 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h={300}>
            <Text fw={600} mb="md">
              Recent Content Performance
            </Text>
            <Stack gap="md">
              <div>
                <Group justify="space-between" mb={5}>
                  <Text size="sm">AI Marketing Blog Post</Text>
                  <Text size="sm" c="dimmed">85% SEO Score</Text>
                </Group>
                <Progress value={85} color="green" size="sm" />
              </div>
              <div>
                <Group justify="space-between" mb={5}>
                  <Text size="sm">LinkedIn Post - Tech Trends</Text>
                  <Text size="sm" c="dimmed">92% SEO Score</Text>
                </Group>
                <Progress value={92} color="blue" size="sm" />
              </div>
              <div>
                <Group justify="space-between" mb={5}>
                  <Text size="sm">Twitter Post - AI Automation</Text>
                  <Text size="sm" c="dimmed">78% SEO Score</Text>
                </Group>
                <Progress value={78} color="yellow" size="sm" />
              </div>
            </Stack>
          </Card>
        </Grid.Col>

        <Grid.Col span={{ base: 12, md: 4 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h={300}>
            <Text fw={600} mb="md">
              Quick Actions
            </Text>
            <Stack gap="sm">
              <Card shadow="xs" padding="sm" radius="sm" withBorder style={{ cursor: 'pointer' }}>
                <Group>
                  <ActionIcon variant="light" color="blue" size="lg">
                    <IconTrendingUp size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Generate Content</Text>
                    <Text size="xs" c="dimmed">Create new AI content</Text>
                  </div>
                </Group>
              </Card>
              
              <Card shadow="xs" padding="sm" radius="sm" withBorder style={{ cursor: 'pointer' }}>
                <Group>
                  <ActionIcon variant="light" color="green" size="lg">
                    <IconEye size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Review Content</Text>
                    <Text size="xs" c="dimmed">3 items pending</Text>
                  </div>
                </Group>
              </Card>
              
              <Card shadow="xs" padding="sm" radius="sm" withBorder style={{ cursor: 'pointer' }}>
                <Group>
                  <ActionIcon variant="light" color="orange" size="lg">
                    <IconShare size={16} />
                  </ActionIcon>
                  <div>
                    <Text size="sm" fw={500}>Schedule Posts</Text>
                    <Text size="xs" c="dimmed">Plan your content</Text>
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