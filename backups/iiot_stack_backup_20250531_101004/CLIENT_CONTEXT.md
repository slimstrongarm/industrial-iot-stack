# Client Context & Requirements

## Client Profile
- **Type**: Real brewery company
- **Owner**: Experienced technical person with existing Node-RED deployment
- **Current Setup**: Already has a Node-RED instance running
- **GitHub**: Will provide access to their repository soon

## Project Status
- **Phase**: POC build for first customer
- **Critical Need**: Production-ready solution when client provides GitHub access
- **Current Challenge**: Memory leak issues in Node-RED flows causing crashes

## Technical Requirements
1. **Scalability**: Must handle production brewery operations without memory issues
2. **Integration**: Connect to existing Node-RED instance
3. **Reliability**: No crashes or memory leaks in 24/7 operation
4. **Deployment**: Ready to deploy immediately upon GitHub access

## Action Items
- [ ] Fix memory leak issues in current flows
- [ ] Prepare migration strategy for client's existing flows
- [ ] Document deployment process for quick implementation
- [ ] Create monitoring for production stability

## Alternative Considerations
- n8n as potential alternative if Node-RED scalability issues persist
- Hybrid approach: Node-RED for edge, n8n for orchestration
- Direct Ignition scripting for critical paths

## Success Criteria
- Zero memory leaks
- < 5 minute deployment time
- Seamless integration with existing setup
- Production-grade reliability

---
*Last Updated: 2025-05-31*